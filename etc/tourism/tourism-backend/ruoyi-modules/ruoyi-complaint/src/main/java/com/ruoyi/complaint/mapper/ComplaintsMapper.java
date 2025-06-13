package com.ruoyi.complaint.mapper;

import java.util.List;
import com.ruoyi.complaint.domain.Complaints;

/**
 * 投诉信息Mapper接口
 * 
 * @author ningf
 * @date 2024-07-15
 */
public interface ComplaintsMapper 
{
    /**
     * 查询投诉信息
     * 
     * @param id 投诉信息主键
     * @return 投诉信息
     */
    public Complaints selectComplaintsById(Long id);

    /**
     * 查询投诉信息列表
     * 
     * @param complaints 投诉信息
     * @return 投诉信息集合
     */
    public List<Complaints> selectComplaintsList(Complaints complaints);

    /**
     * 新增投诉信息
     * 
     * @param complaints 投诉信息
     * @return 结果
     */
    public int insertComplaints(Complaints complaints);

    /**
     * 修改投诉信息
     * 
     * @param complaints 投诉信息
     * @return 结果
     */
    public int updateComplaints(Complaints complaints);

    /**
     * 删除投诉信息
     * 
     * @param id 投诉信息主键
     * @return 结果
     */
    public int deleteComplaintsById(Long id);

    /**
     * 批量删除投诉信息
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteComplaintsByIds(Long[] ids);

    public int confirmComplaintsByIds(Long[] ids);

    public int handleComplaintsById(Long id);
}
