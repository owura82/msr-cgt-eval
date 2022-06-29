//C file
/*
 * Copyright (c) 2016 Hisilicon Limited.
 * Copyright (c) 2007, 2008 Mellanox Technologies. All rights reserved.
 *
 * This software is available to you under a choice of one of two
 * licenses.  You may choose to be licensed under the terms of the GNU
 * General Public License (GPL) Version 2, available from the file
 * COPYING in the main directory of this source tree, or the
 * OpenIB.org BSD license below:
 *
 *     Redistribution and use in source and binary forms, with or
 *     without modification, are permitted provided that the following
 *     conditions are met:
 *
 *      - Redistributions of source code must retain the above
 *        copyright notice, this list of conditions and the following
 *        disclaimer.
 *
 *      - Redistributions in binary form must reproduce the above
 *        copyright notice, this list of conditions and the following
 *        disclaimer in the documentation and/or other materials
 *        provided with the distribution.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */
#include <linux/acpi.h>
#include <linux/of_platform.h>
#include <linux/module.h>
#include <rdma/ib_addr.h>
#include <rdma/ib_smi.h>
#include <rdma/ib_user_verbs.h>
#include <rdma/ib_cache.h>
#include "hns_roce_common.h"
#include "hns_roce_device.h"
#include <rdma/hns-abi.h>
#include "hns_roce_hem.h"

/**
 * hns_get_gid_index - Get gid index.
 * @hr_dev: pointer to structure hns_roce_dev.
 * @port:  port, value range: 0 ~ MAX
 * @gid_index:  gid_index, value range: 0 ~ MAX
 * Description:
 *    N ports shared gids, allocation method as follow:
 *		GID[0][0], GID[1][0],.....GID[N - 1][0],
 *		GID[0][0], GID[1][0],.....GID[N - 1][0],
 *		And so on
 */
int hns_get_gid_index(struct hns_roce_dev *hr_dev, u8 port, int gid_index)
{
	return gid_index * hr_dev->caps.num_ports + port;
}
EXPORT_SYMBOL_GPL(hns_get_gid_index);

static int hns_roce_set_mac(struct hns_roce_dev *hr_dev, u8 port, u8 *addr)
{
	u8 phy_port;
	u32 i = 0;

	if (!memcmp(hr_dev->dev_addr[port], addr, MAC_ADDR_OCTET_NUM))
		return 0;

	for (i = 0; i < MAC_ADDR_OCTET_NUM; i++)
		hr_dev->dev_addr[port][i] = addr[i];

	phy_port = hr_dev->iboe.phy_port[port];
	return hr_dev->hw->set_mac(hr_dev, phy_port, addr);
}

static int hns_roce_add_gid(struct ib_device *device, u8 port_num,
			    unsigned int index, const union ib_gid *gid,
			    const struct ib_gid_attr *attr, void **context)
{
	struct hns_roce_dev *hr_dev = to_hr_dev(device);
	u8 port = port_num - 1;
	unsigned long flags;
	int ret;

	if (port >= hr_dev->caps.num_ports)
		return -EINVAL;

	spin_lock_irqsave(&hr_dev->iboe.lock, flags);

	ret = hr_dev->hw->set_gid(hr_dev, port, index, (union ib_gid *)gid,
				   attr);

	spin_unlock_irqrestore(&hr_dev->iboe.lock, flags);

	return ret;
}

static int hns_roce_del_gid(struct ib_device *device, u8 port_num,
			    unsigned int index, void **context)
{
	struct hns_roce_dev *hr_dev = to_hr_dev(device);
	struct ib_gid_attr zattr = { };
	union ib_gid zgid = { {0} };
	u8 port = port_num - 1;
	unsigned long flags;
	int ret;

	if (port >= hr_dev->caps.num_ports)
		return -EINVAL;

	spin_lock_irqsave(&hr_dev->iboe.lock, flags);

	ret = hr_dev->hw->set_gid(hr_dev, port, index, &zgid, &zattr);

	spin_unlock_irqrestore(&hr_dev->iboe.lock, flags);

	return ret;
}

static int handle_en_event(struct hns_roce_dev *hr_dev, u8 port,
			   unsigned long event)
{
	struct device *dev = hr_dev->dev;
	struct net_device *netdev;
	int ret = 0;

	netdev = hr_dev->iboe.netdevs[port];
	if (!netdev) {
		dev_err(dev, "port(%d) can't find netdev\n", port);
		return -ENODEV;
	}

	switch (event) {
	case NETDEV_UP:
	case NETDEV_CHANGE:
	case NETDEV_REGISTER:
	case NETDEV_CHANGEADDR:
		ret = hns_roce_set_mac(hr_dev, port, netdev->dev_addr);
		break;
	case NETDEV_DOWN:
		/*
		 * In v1 engine, only support all ports closed together.
		 */
		break;
	default:
		dev_dbg(dev, "NETDEV event = 0x%x!\n", (u32)(event));
		break;
	}

	return ret;
}

static int hns_roce_netdev_event(struct notifier_block *self,
				 unsigned long event, void *ptr)
{
	struct net_device *dev = netdev_notifier_info_to_dev(ptr);
	struct hns_roce_ib_iboe *iboe = NULL;
	struct hns_roce_dev *hr_dev = NULL;
	u8 port = 0;
	int ret = 0;

	hr_dev = container_of(self, struct hns_roce_dev, iboe.nb);
	iboe = &hr_dev->iboe;

	for (port = 0; port < hr_dev->caps.num_ports; port++) {
		if (dev == iboe->netdevs[port]) {
			ret = handle_en_event(hr_dev, port, event);
			if (ret)
				return NOTIFY_DONE;
			break;
		}
	}

	return NOTIFY_DONE;
}

static int hns_roce_setup_mtu_mac(struct hns_roce_dev *hr_dev)
{
	int ret;
	u8 i;

	for (i = 0; i < hr_dev->caps.num_ports; i++) {
		if (hr_dev->hw->set_mtu)
			hr_dev->hw->set_mtu(hr_dev, hr_dev->iboe.phy_port[i],
					    hr_dev->caps.max_mtu);
		ret = hns_roce_set_mac(hr_dev, i,
				       hr_dev->iboe.netdevs[i]->dev_addr);
		if (ret)
			return ret;
	}

	return 0;
}

static int hns_roce_query_device(struct ib_device *ib_dev,
				 struct ib_device_attr *props,
				 struct ib_udata *uhw)
{
	struct hns_roce_dev *hr_dev = to_hr_dev(ib_dev);

	memset(props, 0, sizeof(*props));

	props->sys_image_guid = cpu_to_be32(hr_dev->sys_image_guid);
	props->max_mr_size = (u64)(~(0ULL));
	props->page_size_cap = hr_dev->caps.page_size_cap;
	props->vendor_id = hr_dev->vendor_id;
	props->vendor_part_id = hr_dev->vendor_part_id;
	props->hw_ver = hr_dev->hw_rev;
	props->max_qp = hr_dev->caps.num_qps;
	props->max_qp_wr = hr_dev->caps.max_wqes;
	props->device_cap_flags = IB_DEVICE_PORT_ACTIVE_EVENT |
				  IB_DEVICE_RC_RNR_NAK_GEN;
	props->max_sge = max(hr_dev->caps.max_sq_sg, hr_dev->caps.max_rq_sg);
	props->max_sge_rd = 1;
	props->max_cq = hr_dev->caps.num_cqs;
	props->max_cqe = hr_dev->caps.max_cqes;
	props->max_mr = hr_dev->caps.num_mtpts;
	props->max_pd = hr_dev->caps.num_pds;
	props->max_qp_rd_atom = hr_dev->caps.max_qp_dest_rdma;
	props->max_qp_init_rd_atom = hr_dev->caps.max_qp_init_rdma;
	props->atomic_cap = IB_ATOMIC_NONE;
	props->max_pkeys = 1;
	props->local_ca_ack_delay = hr_dev->caps.local_ca_ack_delay;

	return 0;
}

static struct net_device *hns_roce_get_netdev(struct ib_device *ib_dev,
					      u8 port_num)
{
	struct hns_roce_dev *hr_dev = to_hr_dev(ib_dev);
	struct net_device *ndev;

	if (port_num < 1 || port_num > hr_dev->caps.num_ports)
		return NULL;

	rcu_read_lock();

	ndev = hr_dev->iboe.netdevs[port_num - 1];
	if (ndev)
		dev_hold(ndev);

	rcu_read_unlock();
	return ndev;
}

static int hns_roce_query_port(struct ib_device *ib_dev, u8 port_num,
			       struct ib_port_attr *props)
{
	struct hns_roce_dev *hr_dev = to_hr_dev(ib_dev);
	struct device *dev = hr_dev->dev;
	struct net_device *net_dev;
	unsigned long flags;
	enum ib_mtu mtu;
	u8 port;

	assert(port_num > 0);
	port = port_num - 1;

	/* props being zeroed by the caller, avoid zeroing it here */

	props->max_mtu = hr_dev->caps.max_mtu;
	props->gid_tbl_len = hr_dev->caps.gid_table_len[port];
	props->port_cap_flags = IB_PORT_CM_SUP | IB_PORT_REINIT_SUP |
				IB_PORT_VENDOR_CLASS_SUP |
				IB_PORT_BOOT_MGMT_SUP;
	props->max_msg_sz = HNS_ROCE_MAX_MSG_LEN;
	props->pkey_tbl_len = 1;
	props->active_width = IB_WIDTH_4X;
	props->active_speed = 1;

	spin_lock_irqsave(&hr_dev->iboe.lock, flags);

	net_dev = hr_dev->iboe.netdevs[port];
	if (!net_dev) {
		spin_unlock_irqrestore(&hr_dev->iboe.lock, flags);
		dev_err(dev, "find netdev %d failed!\r\n", port);
		return -EINVAL;
	}

	mtu = iboe_get_mtu(net_dev->mtu);
	props->active_mtu = mtu ? min(props->max_mtu, mtu) : IB_MTU_256;
	props->state = (netif_running(net_dev) && netif_carrier_ok(net_dev)) ?
			IB_PORT_ACTIVE : IB_PORT_DOWN;
	props->phys_state = (props->state == IB_PORT_ACTIVE) ? 5 : 3;

	spin_unlock_irqrestore(&hr_dev->iboe.lock, flags);

	return 0;
}

static enum rdma_link_layer hns_roce_get_link_layer(struct ib_device *device,
						    u8 port_num)
{
	return IB_LINK_LAYER_ETHERNET;
}

static int hns_roce_query_gid(struct ib_device *ib_dev, u8 port_num, int index,
			      union ib_gid *gid)
{
	return 0;
}

static int hns_roce_query_pkey(struct ib_device *ib_dev, u8 port, u16 index,
			       u16 *pkey)
{
	*pkey = PKEY_ID;

	return 0;
}

static int hns_roce_modify_device(struct ib_device *ib_dev, int mask,
				  struct ib_device_modify *props)
{
	unsigned long flags;

	if (mask & ~IB_DEVICE_MODIFY_NODE_DESC)
		return -EOPNOTSUPP;

	if (mask & IB_DEVICE_MODIFY_NODE_DESC) {
		spin_lock_irqsave(&to_hr_dev(ib_dev)->sm_lock, flags);
		memcpy(ib_dev->node_desc, props->node_desc, NODE_DESC_SIZE);
		spin_unlock_irqrestore(&to_hr_dev(ib_dev)->sm_lock, flags);
	}

	return 0;
}

static int hns_roce_modify_port(struct ib_device *ib_dev, u8 port_num, int mask,
				struct ib_port_modify *props)
{
	return 0;
}

static struct ib_ucontext *hns_roce_alloc_ucontext(struct ib_device *ib_dev,
						   struct ib_udata *udata)
{
	int ret = 0;
	struct hns_roce_ucontext *context;
  
  //prompt here - check for initialization
  //response
	struct hns_roce_ib_alloc_ucontext_resp resp = {};
